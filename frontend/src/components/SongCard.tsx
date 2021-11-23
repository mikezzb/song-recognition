import { FC } from 'react';
import { Song } from '../types';
import { strToBase64 } from '../utils';
import './SongCard.scss';

type SongCardProps = {
  song: Song;
};

const SongCard: FC<SongCardProps> = ({ song }) => {
  return (
    <div className="song card row">
      <span
        style={{
          backgroundImage: `url("${strToBase64(song.cover)}")`,
        }}
        className="cover"
      />
      <div className="detail column">
        <h3>{song.title}</h3>
        <h4>{song.artist}</h4>
        {Boolean(song.match) && <h5>{`${song.match * 100}% matches`}</h5>}
      </div>
    </div>
  );
};

export default SongCard;
