import React, { useCallback, useEffect, useRef, useState } from "react";
import { getMontlhyBalanceCategories, getMonthlyBalances } from "../common/api"
import { MonthlyBalance, MonthlyBalanceCategory } from "../common/interfaces"
import { Pulldown, BalanceTable } from "./shared"
import { isCorrectFormatDate } from "../common/utilities"

export const MonthlyBalanceTab = () => {
  const [isSending, setIsSending] = useState(false)
  const [data,setData] = useState<Array<MonthlyBalance>>([]);
  // NOTE: This api only accepts YYYY-MM-01 format
  const [month, setMonth] = useState("2020-12-01");

  const fetchData = useCallback(() => {
    if (isSending || !isCorrectFormatDate(month)) return;
    setIsSending(true)

    getMonthlyBalances(month).then(function(data: Array<MonthlyBalance>) {
      setData(data)
      setIsSending(false)
    }).catch((err) => {
      console.log('Failed to fetch page: ', err)
      setIsSending(false)
    })
  }, [month])

  useEffect(()=> {
      fetchData()
  },[fetchData])

  return (
    <div>
      <p>Monthly Blances</p>
      <input type="text" onChange={e => setMonth(e.target.value)} value={month}/>
      <button onClick={fetchData}>{ isSending ? "Fetching..." : "Fetch"}</button>
      { data.length > 1 ? <BalanceTable data={data} /> : null}
    </div>
   )
}
