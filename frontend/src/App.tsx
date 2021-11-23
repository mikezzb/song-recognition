import { FC } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import './App.scss';
import Navigator from './containers';
import './init';
import StoreProvider from './stores';

const queryClient = new QueryClient();

const App: FC = () => (
  <StoreProvider>
    <QueryClientProvider client={queryClient}>
      <Navigator />
    </QueryClientProvider>
  </StoreProvider>
);

export default App;
