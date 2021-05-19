import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppConstants } from '../app-constants';

@Injectable({
  providedIn: 'root'
})
export class BookViewService {

  constructor(private http: HttpClient) { }

  getBookData(mmsId: number): Observable<any> {
    return this.http.get<any>(AppConstants.NLP_REST_BASE + '/getBookData/' + mmsId);
  }
}
