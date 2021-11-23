import { useState } from 'react';
import MicRecorder from 'mic-recorder-to-mp3';
import axios from 'axios';
import { IconButton, Typography } from '@material-ui/core';
import { AudiotrackRounded } from '@material-ui/icons';

import { RECORDER_BIT_RATE, RECORD_SECONDS } from '../configs';
import './HomePage.scss';
import { QUERY_BY_HUMMING, RECOGNIZE } from '../constants/apis';
import Header from '../components/Header';

enum HomePageState {
  INIT,
  RECORDING,
  RECOGNIZING,
}

enum HomePageMode {
  FINGERPRINT,
  QBH,
}

const recorder = new MicRecorder({ bitRate: RECORDER_BIT_RATE });

const HomePage = () => {
  const [state, setState] = useState(HomePageState.INIT);
  const [mode, setMode] = useState(HomePageMode.FINGERPRINT);
  const [result, setResult] = useState(null);

  const recognize = async (file?: File) => {
    setResult(null);
    const audio = file || (await record());
    if (audio === null) {
      return;
    }
    const formData = new FormData();
    formData.append('audio', audio, audio.name);
    const res = await axios({
      ...(mode === HomePageMode.FINGERPRINT ? RECOGNIZE : QUERY_BY_HUMMING),
      data: formData,
    });

    setResult(JSON.stringify(res.data));
    setState(HomePageState.INIT);
  };

  const record = async (): Promise<File | null> => {
    try {
      // Record
      await recorder.start();
      setState(HomePageState.RECORDING);
      await new Promise(resolve => setTimeout(resolve, RECORD_SECONDS * 1000));
      setState(HomePageState.RECOGNIZING);

      // Get file and call API
      const [buffer, blob] = await recorder.stop().getMp3();
      const now = +new Date();
      const file = new File(buffer, `${now}.mp3`, {
        type: blob.type,
        lastModified: now,
      });
      return file;
    } catch (e) {
      alert(e);
      return null;
    }
  };
  return (
    <div className="homepage page center">
      <Header />
      <div className="column center">
        <Typography className="banner-text" variant="h2" component="div">
          Tap to recognize your song
        </Typography>
        {state === HomePageState.INIT && (
          <IconButton className="query-btn" onClick={() => recognize()}>
            <AudiotrackRounded />
          </IconButton>
        )}
      </div>
      {Boolean(result) && <p>{result}</p>}
    </div>
  );
};

export default HomePage;
