import React, { useEffect, useRef, useState } from "react";
import { getCategories, getExpensesByCategoryId } from "../common/api"
import { Category, Expense } from "../common/interfaces"
import { Pulldown, Table } from "./shared"

export const ExpensebyCategoryTab = () => {
  const [isSending, setIsSending] = useState(false);
  const [data, setData] = useState<Array<Expense>>([]);
  const initialRender = useRef(true);
  const [CategoryId, setCategoryId] = useState<number>(1);
  const [categories, setCategories] = useState<Array<Category>>();
  const [start, setstart] = useState<string>("2020-01-01"); // TODO: grab date.year dinamically
  const [end, setend] = useState<string>("2020-12-31");

  const [active, setActive] = useState(0);
  const handleClick = e => {
    const index = parseInt(e.target.id, 0);
    if (index !== active) {
      setActive(index);
    }
  };

  const fetchData = React.useCallback(() => {
    if (isSending || CategoryId === 0) return; // TODO: is === 0 really necessary?
      setIsSending(true);

      getExpensesByCategoryId(CategoryId, start, end)
      .then((data: Array<Expense>) => {
            setData(data)
            setIsSending(false);
      })
      .catch((err) => {
          console.log('Failed to fetch page: ', err);
          setIsSending(false);
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
      <p>Expenses by Category ID</p>
      <input type="text" onChange={e => setstart(e.target.value)} value={start}/>
      <input type="text" onChange={e => setend(e.target.value)} value={end}/>
      { categories ? <Pulldown data={categories} onChange={handleChange} /> : null }
      <button onClick={fetchData}>{ isSending ? "Fetching..." : "Fetch" }</button>
       { data.length > 1 ? <Table data={data} /> : null }
    </div>
  );

};