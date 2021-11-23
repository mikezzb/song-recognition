import { makeObservable, action, observable } from 'mobx';
import { Mode, Song } from '../types';
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

  get fingerprintHistory() {
    return this.history.filter(song => song.mode === Mode.FINGERPRINT);
  }
  get qbhHistory() {
    return this.history.filter(song => song.mode === Mode.QBH);
  }
  get currentHistory() {
    return this.mode === Mode.FINGERPRINT
      ? this.fingerprintHistory
      : this.qbhHistory;
  }

  @action init() {
    this.loadStore();
  }

  @action toggleMode() {
    this.setStore(
      'mode',
      this.mode === Mode.FINGERPRINT ? Mode.QBH : Mode.FINGERPRINT
    );
  }

  @action appendHistory(song: Song) {
    this.setStore('history', [
      ...this.history,
      {
        ...song,
        mode: this.mode,
      },
    ]);
  }
}

export default UserStore;
