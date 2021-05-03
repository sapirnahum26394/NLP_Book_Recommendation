import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { BlockUI, NgBlockUI } from 'ng-block-ui';

@Component({
  selector: 'app-book-view',
  templateUrl: './book-view.component.html',
  styleUrls: ['./book-view.component.css']
})
export class BookViewComponent implements OnInit {

  @BlockUI() blockUI: NgBlockUI;

  similarBooksList: Object[] = [{id:'123',name: 'First Book'} ,{id:'234',name: 'Second Book'} ,{id:'345',name: 'Third Book'} ,{id:'456',name: 'Fourth Book'} ,{id:'567',name: 'Fifth Book'}];
  
  constructor(private router: Router) { 
    this.blockUI.start('Loading...'); // Start blocking
 
    setTimeout(() => {
      this.blockUI.stop(); // Stop blocking
    }, 2000);
  }

  ngOnInit(): void {
    
  }

  navigateToBook(bookId){
    this.router.navigateByUrl('/book-view/' + bookId);
  }

}
