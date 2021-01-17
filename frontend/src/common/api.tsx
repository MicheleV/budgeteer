import { Category, Expense, MonthlyBalanceCategory, MonthlyBalance } from "../common/interfaces"

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
