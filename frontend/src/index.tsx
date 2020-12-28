import React, { FC, useEffect, ReactElement, useRef, useState } from "react";
import ReactDOM, { render } from "react-dom";
import { ExpensebyCategoryTab, ReduceExpensebyCategoryTab, MonthlyBalanceTab, Tabs, Tab, Content } from "./components/tab";


const App = () => {
  const [active, setActive] = useState(0);
  const handleClick = (e: React.MouseEventHandler<HTMLElement>) => {
    const index = parseInt(e.target.id, 0);
    if (index !== active) {
      setActive(index);
    }
  };


  return <div>
      <Tabs>
        <Tab onClick={handleClick} active={active === 0} id={0}>
          Expenses
        </Tab>

        <Tab onClick={handleClick} active={active === 1} id={1}>
          Expenses aggregate
        </Tab>

        <Tab onClick={handleClick} active={active === 1} id={2}>
          Monthly balances
        </Tab>
      </Tabs>
      <>
        <Content active={active === 0}>
          <ExpensebyCategoryTab />
        </Content>
        <Content active={active === 1}>
          <ReduceExpensebyCategoryTab />
        </Content>
        <Content active={active === 2}>
          <MonthlyBalanceTab />
        </Content>
      </>
  </div>
}


ReactDOM.render(
  <App />,
  document.getElementById("root")
);
