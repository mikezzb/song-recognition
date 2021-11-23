export function removeStoreItem(key: string) {
  try {
    localStorage.removeItem(key);
    return true;
  } catch (e) {
    return false;
  }
}

export function getStoreData(key: string) {
  try {
    return JSON.parse(localStorage.getItem(key));
  } catch (e) {
    console.log(`Loading error: ${e}`);
    return '';
  }
}

export function storeData(key: string, value: any) {
  try {
    return localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.log(`Saving error: ${e}`);
    return '';
  }
}

export function clearStore() {
  localStorage.clear();
}
