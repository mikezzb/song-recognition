import { FC } from 'react';
import clsx from 'clsx';
import { QueryHistory, Song } from '../types';
import SongCard from './SongCard';
import './SongList.scss';
import Loading from './Loading';

type SongListProps = {
  songs: Song[] | QueryHistory[];
  wrap?: Boolean;
  loading?: Boolean;
};

const SongList: FC<SongListProps> = ({ songs, wrap, loading }) => {
  if (loading) {
    return <Loading fixed={true} />;
  }
  return (
    <div className={clsx('songs-list column center', wrap && 'wrap')}>
      {!songs || songs?.length == 0 ? (
        <span>No songs yet~</span>
      ) : (
        songs.map(song => (
          <SongCard key={`${song._id}${song.date}${song.title}`} song={song} />
        ))
      )}
    </div>
  );
};

export default SongList;
