import { createContext } from 'react';

import UserStore from './UserStore';

export const userStore = new UserStore();

export const UserContext = createContext(null as UserStore);

export default function StoreProvider({ children }) {
  return (
    <UserContext.Provider value={userStore}>{children}</UserContext.Provider>
  );
}
