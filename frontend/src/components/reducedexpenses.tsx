import React, { useEffect, useRef, useState } from "react";
import { getCategories, getExpensesByCategoryId } from "../common/api"
import { Category, Expense } from "../common/interfaces"
import { aggregateData } from "../common/utilities"
import { ExpenseAggregate } from "../common/interfaces"
import {  Pulldown, ReducedTable } from "./shared"

export const ReduceExpensebyCategoryTab = () => {
  const [isFetching, setisFetching] = useState(false);
  const [data, setData] = useState<Array<ExpenseAggregate>>([]);
  const initialRender = useRef(true);
  const [CategoryId, setCategoryId] = useState<number>(1);
  const [categories, setCategories] = useState<Array<Category>>();
  const [start, setstart] = useState<string>("2020-01-01");
  const [end, setend] = useState<string>("2020-12-31");


  const fetchData = React.useCallback(() => {
    if (isFetching || CategoryId === 0) return;
      setisFetching(true);

      getExpensesByCategoryId(CategoryId, start, end)
      .then((expenses: Array<Expense>) => {
            // Aggregate expenses by note text
            const dataArray = aggregateData(expenses)
            setData(dataArray)

            setisFetching(false);
      })
      .catch((err) => {
          console.log('Failed to fetch page: ', err);
          setisFetching(false);
      });
  },[start,end,CategoryId])

  useEffect(() => {
    if (initialRender.current){
      initialRender.current = false;
      getCategories().then(function (data: Array<Category>) {
        setCategories(data)
      })
    } else {
      fetchData()
    }
  }, [fetchData]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => setCategoryId(parseInt(e.target.value, 10))

  return (
    <div>
      <p>Sum of Expenses by Category ID</p>
      <input type="text" onChange={e => setstart(e.target.value)} value={start}/>
      <input type="text" onChange={e => setend(e.target.value)} value={end}/>
      { categories ? <Pulldown data={categories} onChange={handleChange} /> : null }
      <button onClick={fetchData}>{ isFetching ? "Fetching..." : "Fetch" }</button>
       { data.length > 1 ? <ReducedTable data={data} /> : null }
    </div>
  );

};
