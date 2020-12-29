import { Expense } from "./api"

export const Formatter = new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' })

export const aggregateData = (expenses: Array<Expense>) => {
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