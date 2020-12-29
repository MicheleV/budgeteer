import React, { FC, useEffect, ReactElement, useRef, useState } from "react";
import { Formatter, aggregateData } from "../common/utilities"

export interface Expense {
  id: number;
  amount: number;
  category_id: number;
  category_text: string;
  note: string;
  date: string;
}

export interface Category {
  id: number;
  text: string;
}

export interface MonthlyBalance {
  id: number;
  amount: number;
  category_id: number;
  category_text: string;
  date: string;
}

export interface MonthlyBalanceCategory {
  id: number;
  amount: number;
  category_id: number;
  category_text: string;
  date: string;
}

export type ExpenseAggregate = {
  label: string;
  amount: number;
}

export type TableProps = {
  data: Array<Expense>
}

export type BalanceTableProps = {
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