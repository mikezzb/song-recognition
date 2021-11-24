export enum Mode {
  FINGERPRINT,
  QBH,
}

export interface Song {
  _id: string;
  album: string;
  artist: string;
  genre: string;
  title: string;
  cover: string;
  year: string;
  ext: string;
  match?: number;
  offset?: number;
}

export interface QueryHistory extends Song {
  mode: Mode;
  date: number;
}
