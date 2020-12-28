import React, { FC, useEffect, ReactElement, useRef, useState } from "react";
import ReactDOM, { render } from "react-dom";
import {Category, Expense, getCategories, getExpensesByCategoryId } from "../common/api"
import {Formatter} from "../common/utilities"

type ExpenseAggregate = {
  label: string;
  amount: number;
}

type TableProps = {
  data: Array<Expense>
}

type PulldownProps = {
  data: Array<Category>;
  onChange: Function; // TODO: shouldn't this be React.ChangeEvent<HTMLSelectElement> ?
}

type ReducedTableProps = {
  data: Array<ExpenseAggregate>
}


const Table: FC<TableProps> = ({data}): ReactElement => {
  const list = data.map(item => {
    return (
      <li key={item.id}>
        {item.category_text}: {Formatter.format(item.amount)}{ item.note !== '' ? `, (${item.note})` : null} - {item.date}
      </li>
    );
  });
  const total = data.reduce((acc, curr) => acc + curr.amount, 0)
  return <div>
    <div>Total: {Formatter.format(total)}</div>
    <ul>{list}</ul>
  </div>
}


const Pulldown: FC<PulldownProps> = ({data, onChange}) : ReactElement => {
  let optionItems = data.map((cat) =>
      <option key={cat.id} value={cat.id}>{cat.text}</option>
  );
  return (
   <div>
       <select onChange={onChange} >
          {optionItems}
       </select>
   </div>
  )
}

export const ExpensebyCategoryTab = () => {
  const [isSending, setIsSending] = useState(false);
  const [data, setData] = useState<Array<Expense>>([]);
  const initialRender = useRef(true);
  const [CategoryId, setCategoryId] = useState<number>(1);
  const [categories, setCategories] = useState<Array<Category>>();
  const [start, setstart] = useState<string>("2020-01-01");
  const [end, setend] = useState<string>("2020-12-31");

  const [active, setActive] = useState(0);
  const handleClick = e => {
    const index = parseInt(e.target.id, 0);
    if (index !== active) {
      setActive(index);
    }
  };

  const fetchData = React.useCallback(() => {
    if (isSending || CategoryId === 0) return;
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


const ReducedTable: FC<ReducedTableProps> = ({data}): ReactElement => {
  const list = data.map((item) => {
    return (
      <li key={item.label}>{item.label} : {Formatter.format(item.amount)}</li>
    );
  });
  const total = data.reduce((acc, curr) => acc + curr.amount, 0)
  return <div>
    <div>Total: {Formatter.format(total)}</div>
    <ul>{list}</ul>
  </div>
}


const aggregateData = (expenses: Array<Expense>) => {
    const data: any = {}

    // Aggregate expenses by note text: produces a dictionary
    expenses.forEach((el: Expense) => {
      if (data[el.note] === undefined){
        data[el.note] = el.amount
      } else {
        data[el.note] += el.amount
      }
    })

    // Convert the dictionary in an array of objects
    return Object.keys(data).map((key) => { return {"label":key, "amount": data[key]}})
}

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

export const MonthlyBalanceTab = () => {
  return (
    <div>Placeholder</div>
   )
}

// Styled components

// Credits https://codesandbox.io/s/react-tabs-with-hooks-and-styled-components-b9z7v?from-embed=&file=/src/index.js:465-885
import styled from "styled-components";
export const Tabs = styled.div`
  overflow: hidden;
  background: #fff;
`;

export const Tab = styled.button`
  border: none;
  outline: none;
  cursor: pointer;
  position: relative;

  margin-right: 0.1em;
  font-size: 1em;
  border: ${props => (props.active ? "1px solid #ccc" : "")};
  border-bottom: ${props => (props.active ? "none" : "")};
  background-color: ${props => (props.active ? "white" : "lightgray")};
  height: ${props => (props.active ? "3em" : "2.6em; top:.4em")};
  transition: background-color 0.5s ease-in-out;

  :hover {
    background-color: white;
  }
`;

export const Content = styled.div`
  ${props => (props.active ? "" : "display:none")}
`;

