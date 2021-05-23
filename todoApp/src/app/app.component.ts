import { Component, OnInit } from '@angular/core';
import { DataService } from './data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'todoApp';
  constructor(public todoService: DataService) {
  }
  addTodo(t: string, d: string): void {
    if (t.trim().length === 0) {
      return;
    }
    this.todoService.addTodo(t, d);
  }
  todoSubmit(t: string, d: string): void {
   return;
  }
  todoComplete(id: string): void {
    this.todoService.completeTodo(id);
  }
  todoDelete(id: string): void {
    this.todoService.deleteTodo(id);
  }
}
