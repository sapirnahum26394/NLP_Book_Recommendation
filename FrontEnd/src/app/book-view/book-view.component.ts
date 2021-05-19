import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BlockUI, NgBlockUI } from 'ng-block-ui';
import { Subscription } from 'rxjs';
import { BookViewService } from './book-view.service';

@Component({
  selector: 'app-book-view',
  templateUrl: './book-view.component.html',
  styleUrls: ['./book-view.component.css']
})
export class BookViewComponent implements OnInit,OnDestroy {

  @BlockUI() blockUI: NgBlockUI;

  private sub = new Subscription();

  similarBooksList: Object[] = [{id:'123',name: 'First Book'} ,{id:'234',name: 'Second Book'} ,{id:'345',name: 'Third Book'} ,{id:'456',name: 'Fourth Book'} ,{id:'567',name: 'Fifth Book'}];
  
  constructor(private router: Router,
              private bookViewService: BookViewService,
              private activatedRoute: ActivatedRoute) { 

  }

  ngOnInit(): void {
    this.blockUI.start('Loading...'); // Start blocking

    this.sub.add(this.bookViewService.getBookData(this.activatedRoute.snapshot.params.id).subscribe(response => {
      this.blockUI.stop();
    }));
  }

  ngOnDestroy() {
    // avoid memory leaks here by cleaning up after ourselves. If we
    // don't then we will continue to run our initialiseInvites()
    // method on every navigationEnd event.
    this.sub.unsubscribe();
  }

  navigateToBook(bookId){
    this.router.navigateByUrl('/book-view/' + bookId);
  }

}
