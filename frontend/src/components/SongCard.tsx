import { FC } from 'react';
import { Song, QueryHistory } from '../types';
import { strToBase64, getMMMDD } from '../utils';
import './SongCard.scss';

type SongCardProps = {
  song: QueryHistory | Song;
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
        <h4 className="ellipsis-text">{song.artist}</h4>
        <h5 className="ellipsis-text">
          {'date' in song
            ? getMMMDD(song.date)
            : `${song.genre} (${song.year})`}
        </h5>
        {/* Boolean(song.match) && <h5>{`${song.match * 100}% matches`}</h5> */}
      </div>
    </div>
  );
};

export default SongCard;
