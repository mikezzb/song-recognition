import { FC } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import './App.scss';
import Navigator from './containers';

const queryClient = new QueryClient();

const App: FC = () => (
  <QueryClientProvider client={queryClient}>
    <Navigator />
  </QueryClientProvider>
);

export default App;
