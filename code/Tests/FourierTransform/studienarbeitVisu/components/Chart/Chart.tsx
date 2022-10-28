import { Component } from "react";
import { CartesianGrid, Legend, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from "recharts";
import { ISpeakerChartRow, IChartValuePair, IWordChartRow } from '../../interfaces/interface'
import { scaleLog } from 'd3-scale'
import styles from "./Chart.module.css";

export interface ChartState {

}

export interface ChartProps {
  speakerData?: ISpeakerChartRow[];
  wordData?: IWordChartRow[];
}

export class Chart extends Component<ChartProps, ChartState> {
  constructor(props: ChartProps) {
    super(props);
  }

  private CustomTooltip = (e) => {
    if (e.active && e.payload && e.payload.length) {
      console.log(e)
      return (
        <div className="custom-tooltip">
          <p className="label">{`${e.label} : ${e.payload[0].value}`}</p>
          <p className="desc">Name: {}</p>
        </div>
      );
    }
  
    return null;
  };

  // array with 24 different color strings
  private colors = [
    '#FF6633',
    '#FFB399',
    '#FF33FF',
    '#FFFF99',
    '#00B3E6',
    '#E6B333',
    '#3366E6',
    '#999966',
    '#99FF99',
    '#B34D4D',
    '#80B300',
    '#809900',
    '#E6B3B3',
    '#6680B3',
    '#66991A',
    '#FF99E6',
    '#CCFF1A',
    '#FF1A66',
    '#E6331A',
    '#33FFCC',
    '#66994D',
    '#B366CC',
    '#4D8000',
    '#B33300',
    '#CC80CC',
    '#66664D',
    '#991AFF',
    '#E666FF',
    '#4DB3FF',
    '#1AB399',
  ]

  render() {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart
          margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
          }}
        >
          <CartesianGrid />
          <XAxis type="number" dataKey="x" name="stature" unit="Hz" domain={['0', '100']} />
          <YAxis type="number" dataKey="y" name="weight" />
          {/* Show name in tooltip */}
          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={this.CustomTooltip} />
          <Legend layout="vertical" verticalAlign="middle" align="right" wrapperStyle={{ paddingLeft: "15px" }}/>
          {
            this.props.speakerData?.map((line, lineId) => {
              console.log(line)
              return (
                <Scatter key={lineId} name={"" + line.word} data={line.frequencies.map((valuePair, valuePairId) => ({...valuePair, y: /*valuePair.y +*/ lineId * 0.001}))} fill={this.colors[lineId % this.colors.length]} line />
              )
            })
          }
          {
            this.props.wordData?.map((line, lineId) => {
              console.log(line)
              return (
                <Scatter key={lineId} name={"" + line.speakerId} data={line.frequencies.map((valuePair, valuePairId) => ({...valuePair, y: /*valuePair.y +*/ lineId * 0.001}))} fill={this.colors[lineId % this.colors.length]} line />
              )
            })
          }
        </ScatterChart>
      </ResponsiveContainer>
    );
  }
}