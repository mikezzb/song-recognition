import { FC } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import HomePage from './HomePage';

const ROUTES = [
  {
    props: {
      exact: true,
      path: '',
      component: HomePage,
    },
  },
];

const Navigator: FC = () => (
  <Router>
    <div className="App">
      <Switch>
        {ROUTES.map(route => (
          <Route key={JSON.stringify(route?.props?.path)} {...route.props} />
        ))}
      </Switch>
    </div>
  </Router>
);

export default Navigator;
