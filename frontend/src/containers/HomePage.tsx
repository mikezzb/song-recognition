import { useState } from 'react';
import MicRecorder from 'mic-recorder-to-mp3';
import axios from 'axios';
import { RECORDER_BIT_RATE, RECORD_SECONDS } from '../configs';
import './HomePage.scss';
import { RECOGNIZE } from '../constants/apis';

enum HomePageState {
  INIT,
  RECORDING,
  RECOGNIZING,
}

const recorder = new MicRecorder({ bitRate: RECORDER_BIT_RATE });

const HomePage = () => {
  const [state, setState] = useState(HomePageState.INIT);
  const [audioURL, setAudioURL] = useState(null);
  const [result, setResult] = useState(null);
  const record = async () => {
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

      const path = URL.createObjectURL(file);

      // Remove later
      const link = document.createElement('a');
      // create a blobURI pointing to our Blob
      link.href = path;
      link.download = file.name;
      // some browser needs the anchor to be in the doc
      document.body.append(link);
      link.click();
      link.remove();

      console.log(path);
      setAudioURL(path);
      const formData = new FormData();
      formData.append('audio', file, file.name);
      const res = await axios({
        ...RECOGNIZE,
        data: formData,
      });

      setResult(JSON.stringify(res.data));

      setState(HomePageState.INIT);
    } catch (e) {
      alert(e);
    }
  };
  return (
    <div className="homepage">
      {state === HomePageState.INIT && <button onClick={record}>Record</button>}
      {Boolean(audioURL) && (
        <audio controls controlsList="download">
          <source src={audioURL} type="audio/mpeg" />
        </audio>
      )}
      {Boolean(result) && <p>{result}</p>}
    </div>
  );
};

export default HomePage;
