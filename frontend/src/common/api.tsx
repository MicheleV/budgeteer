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


export function getExpensesByCategoryId(category_id:number, start:string, end:string): Promise<Expense[]> {
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
