import { Expense } from "./interfaces"

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

export const isCorrectFormatDate = (date: string): Boolean => {
  // NOTE: Many apis only accept YYYY-MM-01 format
  // Only accepts dates between 1000 and 2999: edit this regex if using historical data, of if you are in year 3000+
  const date_regex = /^(1|2)\d{3}-(0[1-9]|1[0-2])-01$/g;
  return date_regex.test(date)
}