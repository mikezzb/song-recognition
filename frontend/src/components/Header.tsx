import { HistoryRounded, LibraryMusicRounded } from '@material-ui/icons';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { useUser } from '../hooks';
import { Mode } from '../types';
import './Header.scss';
import Logo from './Logo';
import ModeSwitch from './ModeSwitch';

const NAV_ITEMS = [
  {
    icon: <LibraryMusicRounded />,
    to: '/song',
  },
  {
    icon: <HistoryRounded />,
    to: '/history',
  },
];

const Header = () => {
  const user = useUser();
  return (
    <header className="row">
      <Logo />
      <nav className="nav-container row center">
        <ModeSwitch
          checked={user.mode === Mode.QBH}
          onClick={() => user.toggleMode()}
        />
        {NAV_ITEMS.map(item => (
          <Link key={item.to} to={item.to}>
            {item.icon}
          </Link>
        ))}
      </nav>
    </header>
  );
};

export default observer(Header);
