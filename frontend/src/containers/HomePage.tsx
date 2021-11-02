import { useState } from 'react';
import MicRecorder from 'mic-recorder-to-mp3';
import { RECORDER_BIT_RATE, RECORD_SECONDS } from '../configs';
import './HomePage.scss';

const recorder = new MicRecorder({ bitRate: RECORDER_BIT_RATE });

const HomePage = () => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const record = async () => {
    try {
      await recorder.start();
      setRecording(true);
      await new Promise(resolve => setTimeout(resolve, RECORD_SECONDS * 1000));
      setRecording(false);
      const [buffer, blob] = await recorder.stop().getMp3();
      const file = new File(buffer, 'me-at-thevoice.mp3', {
        type: blob.type,
        lastModified: +new Date(),
      });
      setAudioURL(URL.createObjectURL(file));
    } catch (e) {
      alert(e);
    }
  };
  return (
    <div className="homepage">
      {!recording && <button onClick={record}>Record</button>}
      {Boolean(audioURL) && (
        <audio controls>
          <source src={audioURL} type="audio/mpeg" />
        </audio>
      )}
    </div>
  );
};

export default HomePage;
