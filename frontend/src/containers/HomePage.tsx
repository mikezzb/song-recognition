import { useCallback, useState } from 'react';
import MicRecorder from 'mic-recorder-to-mp3';
import axios from 'axios';
import { Button, IconButton, Typography } from '@material-ui/core';
import { AudiotrackRounded, GraphicEqRounded } from '@material-ui/icons';
import clsx from 'clsx';
import { observer } from 'mobx-react-lite';
import { useDropzone } from 'react-dropzone';
import { RECORDER_BIT_RATE, RECORD_SECONDS } from '../configs';
import './HomePage.scss';
import { QUERY_BY_HUMMING, RECOGNIZE } from '../constants/apis';
import { useUser } from '../hooks';
import { Mode, Song } from '../types';
import SongList from '../components/SongList';

enum HomePageState {
  INIT,
  RECORDING,
  RECOGNIZING,
  RESULT,
}

const recorder = new MicRecorder({ bitRate: RECORDER_BIT_RATE });

const PHRASES = {
  [HomePageState.RECORDING]: 'Recording...',
  [HomePageState.RECOGNIZING]: 'Just a moment...',
};

const HomePage = () => {
  const [state, setState] = useState(HomePageState.INIT);
  const [result, setResult] = useState<null | Song[]>(null);
  const user = useUser();

  const onDrop = useCallback(files => {
    recognize(files[0]);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    noClick: true,
  });

  const recognize = async (file?: File) => {
    const audio = file || (await record());
    setState(HomePageState.RECOGNIZING);
    if (audio === null) {
      return;
    }
    const formData = new FormData();
    formData.append('audio', audio, audio.name);
    const res = await axios({
      ...(user.mode === Mode.FINGERPRINT ? RECOGNIZE : QUERY_BY_HUMMING),
      data: formData,
    });

    setResult(res.data);
    setState(HomePageState.RESULT);
    if (res.data && res.data.length !== 0) {
      user.appendHistory(res.data[0]);
    }
  };

  const record = async (): Promise<File | null> => {
    try {
      // Record
      await recorder.start();
      setState(HomePageState.RECORDING);
      await new Promise(resolve => setTimeout(resolve, RECORD_SECONDS * 1000));
      // Get file and call API
      const [buffer, blob] = await recorder.stop().getMp3();
      const now = +new Date();
      const file = new File(buffer, `${now}.mp3`, {
        type: blob.type,
        lastModified: now,
      });

      // Remove later
      const link = document.createElement('a');
      // create a blobURI pointing to our Blob
      const path = URL.createObjectURL(file);
      link.href = path;
      link.download = file.name;
      // some browser needs the anchor to be in the doc
      document.body.append(link);
      link.click();
      link.remove();
      return file;
    } catch (e) {
      alert(e);
      return null;
    }
  };
  return (
    <div className="homepage page center column" {...getRootProps()}>
      <div className="column center">
        {state !== HomePageState.RESULT && (
          <>
            <Typography
              className={clsx(
                'banner-text',
                state === HomePageState.INIT && 'deco-line'
              )}
              variant="h2"
              component="div"
            >
              {state === HomePageState.INIT
                ? `Tap to recognize your ${
                    user.mode === Mode.FINGERPRINT ? 'song' : 'humming'
                  }`
                : PHRASES[state]}
            </Typography>
            <IconButton className="query-btn" onClick={() => recognize()}>
              {user.mode === Mode.FINGERPRINT ? (
                <AudiotrackRounded />
              ) : (
                <GraphicEqRounded />
              )}
            </IconButton>
          </>
        )}
      </div>
      {state === HomePageState.RESULT && (
        <>
          {result?.length ? (
            <SongList songs={result} />
          ) : (
            <span>Unable to identify the song...</span>
          )}
          <Button
            color="secondary"
            variant="contained"
            className="try-btn"
            onClick={() => recognize()}
          >
            Try Again
          </Button>
        </>
      )}
      <input {...getInputProps()} />
    </div>
  );
};

export default observer(HomePage);
