import {
  HistoryRounded,
  LibraryMusicRounded,
  RecordVoiceOverRounded,
} from '@material-ui/icons';
import { Link } from 'react-router-dom';
import './Header.scss';
import Logo from './Logo';

const NAV_ITEMS = [
  {
    icon: <RecordVoiceOverRounded />,
    to: '/humming',
  },
  {
    icon: <LibraryMusicRounded />,
    to: '/song',
  },
  {
    icon: <HistoryRounded />,
    to: '/history',
  },
];

const Header = () => (
  <header className="row">
    <Logo />
    <nav className="nav-container row center">
      {NAV_ITEMS.map(item => (
        <Link key={item.to} to={item.to}>
          {item.icon}
        </Link>
      ))}
    </nav>
  </header>
);

export default Header;
