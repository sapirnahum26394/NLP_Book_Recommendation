import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AppConstants } from '../app-constants';

@Component({
  selector: 'app-find-similar-books',
  templateUrl: './find-similar-books.component.html',
  styleUrls: ['./find-similar-books.component.scss']
})
export class FindSimilarBooksComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  afuConfig = {
    uploadAPI: {
      url: AppConstants.NLP_REST_BASE + '/addNewBook'
    },
    replaceTexts: {
      selectFileBtn: 'Select MARC21 File',
      resetBtn: 'Reset',
      uploadBtn: 'Upload',
      attachPinBtn: 'Attach Files...',
      afterUploadMsg_success: 'Successfully Uploaded !',
      afterUploadMsg_error: 'Upload Failed !',
      sizeLimit: 'Size Limit'
    }
  };

  fileUploaded(event){
    if(event.status===200){
      this.router.navigateByUrl('/data-table')
    }
  }
}
