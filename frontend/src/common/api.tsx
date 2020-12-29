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


export function getExpensesByCategoryId(category_id:number, start:string, end:string): Promise<Expense[]> {
  // TODO: validate parameters!
  return fetch(`/api/expenses?category_id=${category_id}&format=json&huge_page=yes&start=${start}&end=${end}`)
    .then(function(response) {
      return response.json();
  })
}

export function getCategories(): Promise<Category[]> {
  return fetch('/api/categories')
    .then(function(response) {
      return response.json();
  })
}


export function getMontlhyBalanceCategories(): Promise<MonthlyBalanceCategory[]> {
  return fetch('/api/monthly_balance_categories')
    .then(function(response) {
      return response.json();
  })
}

export function getMonthlyBalances(date?:string): Promise<MonthlyBalance[]> {
  let url = "/api/monthly_balances"
  // TODO: validate parameters!
  if (date) {
    url += `?date=${date}`
  }
  return fetch(url)
    .then(function(response) {
      return response.json();
  })
}
