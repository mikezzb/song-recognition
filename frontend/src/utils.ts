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

export const strToBase64 = (str: string) => `data:image/png;base64, ${str}`;

const MONTHS = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
];

const addZero = (digit: number) => (digit > 9 ? digit : `0${digit}`);

export const getMMMDD = (timestamp: number) => {
  const date = new Date(timestamp);
  return `${MONTHS[date.getMonth()]} ${date.getDate()}, ${addZero(
    date.getHours()
  )}:${addZero(date.getMinutes())}`;
};
