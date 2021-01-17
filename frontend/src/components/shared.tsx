import React, { FC, ReactElement } from "react";
import { Formatter } from "../common/utilities"
import { getCategories, getExpensesByCategoryId } from "../common/api"
import { Category, Expense, BalanceTableProps, ExpenseAggregate, TableProps, PulldownProps, ReducedTableProps } from "../common/interfaces"


export const Pulldown: FC<PulldownProps> = ({data, onChange}) : ReactElement => {
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

export const Table: FC<TableProps> = ({data}): ReactElement => {
  const list = data.map(item => {
    return (
      <li key={item.id}>
        {item.date}: {Formatter.format(item.amount)}{ item.note !== '' ? `, (${item.note})` : null}
      </li>
    );
  });
  const total = data.reduce((acc, curr) => acc + curr.amount, 0)
  return <div>
    <div>Total: {Formatter.format(total)}</div>
    <ul>{list}</ul>
  </div>
}

export const BalanceTable: FC<BalanceTableProps> = ({data}): ReactElement => {
  const list = data.map(item => {
    return (
      <li key={item.id}>
        {item.category_text}: {Formatter.format(item.amount)}
      </li>
    );
  });
  const total = data.reduce((acc, curr) => acc + curr.amount, 0)
  return <div>
    <div>Total: {Formatter.format(total)}</div>
    <ul>{list}</ul>
  </div>
}

export const ReducedTable: FC<ReducedTableProps> = ({data}): ReactElement => {
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

