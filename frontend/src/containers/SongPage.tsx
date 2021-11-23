import axios from 'axios';
import { useQuery } from 'react-query';
import { useLocation } from 'react-router-dom';
import { GET_SONGS } from '../constants/apis';
import { useUser } from '../hooks';
import './SongPage.scss';
import SongList from '../components/SongList';

const SongPage = () => {
  const user = useUser();
  const location = useLocation();
  const { data: songs, isLoading: songsLoading } = useQuery({
    queryKey: GET_SONGS.url,
    queryFn: async () => {
      const res = await axios(GET_SONGS);
      return res.data;
    },
    enabled: location.pathname === '/song',
  });
  return (
    <div className="page">
      <SongList
        wrap
        loading={songsLoading}
        songs={location.pathname === '/song' ? songs : user.currentHistory}
      />
    </div>
  );
};

export default SongPage;
