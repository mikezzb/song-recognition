import { FC } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Header from '../components/Header';
import HomePage from './HomePage';
import SongPage from './SongPage';
import './index.scss';

const ROUTES = [
  {
    props: {
      exact: true,
      path: '/',
      component: HomePage,
    },
  },
  {
    props: {
      exact: true,
      path: ['/history', '/song'],
      component: SongPage,
    },
  },
];

const Navigator: FC = () => (
  <Router>
    <div className="App">
    <Header />
      <Switch>
        {ROUTES.map(route => (
          <Route key={JSON.stringify(route?.props?.path)} {...route.props} />
        ))}
      </Switch>
    </div>
  </Router>
);

export default Navigator;
