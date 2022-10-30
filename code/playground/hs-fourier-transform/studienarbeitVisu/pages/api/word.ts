// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import mysql from 'serverless-mysql'
import { IWordChartRow } from '../../interfaces/interface';

type Data = {
  data: IWordChartRow[]
}

export default async function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  const word = req.body.word;

  const db = mysql({
    config: {
      host: process.env.MYSQL_HOST,
      database: process.env.MYSQL_DATABASE,
      user: process.env.MYSQL_USER,
      password: process.env.MYSQL_PASSWORD,
    },
  })

  const result: IWordChartRow[] = await db.query(`SELECT datensatz.speakerId, datensatz.id, GROUP_CONCAT(JSON_OBJECT('x', frequenz.frequenz, 'y', frequenz.amplitude)) as frequencies FROM datensatz JOIN frequenz ON datensatz.id = frequenz.datensatzId WHERE word LIKE '${word}' AND speakerId < 100 GROUP BY datensatz.speakerId ORDER BY frequenz.frequenz AND datensatz.speakerId`)

  for (const element of result) {
    element.frequencies = JSON.parse("[" + element.frequencies + "]")
  }

  await db.end()

  res.status(200).json({ data: result })
}
