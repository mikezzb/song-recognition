import { action } from 'mobx';
import { getStoreData, removeStoreItem, storeData } from '../utils';

class StorePrototype {
  onLoadKeys?: string[];
  onResetKeys?: string[];
  defaultValues?: Record<string, any>;

  constructor(
    onLoadKeys?: string[],
    onResetKeys?: string[],
    defaultValues?: Record<string, any>
  ) {
    this.onLoadKeys = onLoadKeys;
    this.onResetKeys = onResetKeys;
    this.defaultValues = defaultValues;
  }

  @action.bound updateStore(key: string, value: any) {
    this[key] = value;
  }

  @action loadStore = () => {
    const defaultValues = { ...this.defaultValues };
    if (this.onLoadKeys) {
      this.onLoadKeys.map(async key => {
        const retrieved = getStoreData(key);
        this.updateStore(
          key,
          retrieved === null ? (this.defaultValues || {})[key] : retrieved
        );
        delete defaultValues[key];
      });
    }
    this.initStore(defaultValues);
  };

  @action setStore = async (key: string, value: any) => {
    this.updateStore(key, value);
    storeData(key, value);
  };

  @action resetStore = async () => {
    const defaultValues = { ...this.defaultValues };
    if (this.onResetKeys) {
      this.onResetKeys.map(async key => {
        removeStoreItem(key);
        this.updateStore(key, (this.defaultValues || {})[key] || null);
        delete defaultValues[key];
      });
    }
    this.initStore(defaultValues);
  };

  @action initStore = (defaultValues?: Record<string, any>) => {
    if (this.defaultValues) {
      Object.entries(defaultValues || this.defaultValues).forEach(([k, v]) => {
        this.updateStore(k, v);
      });
    }
  };
}

export default StorePrototype;
