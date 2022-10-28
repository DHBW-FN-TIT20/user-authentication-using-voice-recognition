// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import mysql from 'serverless-mysql'
import { ISpeakerChartRow } from '../../interfaces/interface';

type Data = {
  data: ISpeakerChartRow[]
}

export default async function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  const speakerId = req.body.speakerId;

  const db = mysql({
    config: {
      host: process.env.MYSQL_HOST,
      database: process.env.MYSQL_DATABASE,
      user: process.env.MYSQL_USER,
      password: process.env.MYSQL_PASSWORD,
    },
  })

  const result: ISpeakerChartRow[] = await db.query(`SELECT datensatz.word, datensatz.id, GROUP_CONCAT(JSON_OBJECT('x', frequenz.frequenz, 'y', frequenz.amplitude)) as frequencies FROM datensatz JOIN frequenz ON datensatz.id = frequenz.datensatzId WHERE speakerID = ${speakerId} GROUP BY datensatz.word ORDER BY frequenz.frequenz`)

  for (const element of result) {
    element.frequencies = JSON.parse("[" + element.frequencies + "]")
  }

  await db.end()

  res.status(200).json({ data: result })
}
