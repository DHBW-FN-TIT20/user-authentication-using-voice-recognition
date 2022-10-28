export interface ISpeakerChartRow {
  word: string;
  id: number;
  frequencies: IChartValuePair[];
}

export interface IWordChartRow {
  speakerId: number;
  id: number;
  frequencies: IChartValuePair[];
}

export interface IChartValuePair {
  x: number;
  y: number;
}