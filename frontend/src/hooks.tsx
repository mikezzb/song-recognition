import { useContext } from 'react';
import { UserContext } from './stores';

export const useUser = () => useContext(UserContext);
