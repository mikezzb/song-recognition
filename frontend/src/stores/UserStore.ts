import { makeObservable, action, observable } from 'mobx';
import { Mode } from '../types';
import StorePrototype from './StorePrototype';

const LOAD_KEYS = ['history', 'mode'];

const RESET_KEYS = LOAD_KEYS;

const DEFAULT_VALUES = {
  history: [],
  mode: Mode.FINGERPRINT,
};

class UserStore extends StorePrototype {
  @observable mode: Mode;
  @observable history: Record<string, any>[];

  constructor() {
    super(LOAD_KEYS, RESET_KEYS, DEFAULT_VALUES);
    this.init();
    makeObservable(this);
  }

  @action async init() {
    this.loadStore();
  }

  get fingerprintHistory() {
    return this.history.filter(song => song.mode === Mode.FINGERPRINT);
  }
  get qbhHistory() {
    return this.history.filter(song => song.mode === Mode.QBH);
  }
}

export default UserStore;
