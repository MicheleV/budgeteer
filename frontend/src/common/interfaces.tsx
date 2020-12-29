import React, { FC, useEffect, ReactElement, useRef, useState } from "react";
import { Category, Expense } from "../common/api"
import { Formatter, aggregateData } from "../common/utilities"

export type ExpenseAggregate = {
  label: string;
  amount: number;
}

export type TableProps = {
  data: Array<Expense>
}

export type PulldownProps = {
  data: Array<Category>;
 // TODO: shouldn't onChange be React.ChangeEvent<HTMLSelectElement> instead?
  onChange: Function;
}

export type ReducedTableProps = {
  data: Array<ExpenseAggregate>
}