import { Injectable } from '@angular/core';
import { Todo } from './todo';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http'
import { catchError, debounce } from 'rxjs/operators';
import { throwError as observableThrowError } from 'rxjs';

const API_URL = 'http://127.0.0.1:5005';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  todoList: Todo[] = [];
  constructor(private http: HttpClient) {
    this.todoList = this.getTodoList();
  }
  getTodoList(): Todo[] {
    this.http.get(API_URL + '/todoList')
      .pipe(catchError(this.errorHandler))
      .subscribe((response: any) => {
        console.log(response);
        
        this.todoList = response;
      })
    return this.todoList;
  }

  errorHandler(error: HttpErrorResponse) {
    return observableThrowError(error.message || 'Something went wrong!');
  }

  addTodo(todoTitle: string, todoDescription: string): void {
    if (todoTitle.trim().length === 0) {
      return;
    }
    const headers = new HttpHeaders({
      "Content-Type": "application/json",
    });
    const item={
      title: todoTitle,
      description: todoDescription
    }
    this.http.post(API_URL+'/todoList', JSON.stringify(item), {headers})
      .subscribe((response: any) => {
        this.getTodoList();
      });
  }

  
  deleteTodo(id:string): void {
    this.http.delete(API_URL + '/todoList/' + id)
    .subscribe((response: any) => {
      this.getTodoList();
      })
  }

  completeTodo(id:string): void {
    const headers = new HttpHeaders({
      "Content-Type": "application/json",
    });
    const item={
      _id: id
    }
    this.http.put(API_URL + '/todoList', JSON.stringify(item), {headers})
    .subscribe((response: any) => {
      this.getTodoList();
      })
  }
}
