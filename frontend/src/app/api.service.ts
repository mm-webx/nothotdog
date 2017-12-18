import {Injectable} from "@angular/core";
import "rxjs/add/observable/of";
import "rxjs/add/operator/do";
import "rxjs/add/operator/delay";
import {User} from "./_models/user.model";
import {Router} from "@angular/router";
import {environment} from "../environments/environment";
import {CookieService} from "ngx-cookie";
import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {catchError, tap} from "rxjs/operators";
import {Observable} from "rxjs/Observable";
import {Picture} from "./_models/picture.model";

@Injectable()
export class ApiService {
  public user: User;
  public isLoggedIn: boolean = false;
  public picture: Picture = new Picture;
  public uploading: boolean = false;
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private router: Router, private _cookieService: CookieService) {
    this.user = new User;
    this.user.token = this._cookieService.get('user-token');
    if (this.user.token) {
      this.isLoggedIn = true;
    }
  }

  getHeaders() {
    if (this.user.token) {
      return {
        headers: new HttpHeaders({
          'Authorization': 'JWT ' + this.user.token,
          'Content-Type': 'application/json'
        })
      }
    }

    return {headers: new HttpHeaders({'Content-Type': 'application/json'})}
  }

  logout(navigate = false) {
    this.user = new User;
    this._cookieService.remove('user-token');
    this.isLoggedIn = false;
    if (navigate) {
      this.router.navigate(['/']);
    }
  }

  postAuth(): Observable<{}> {
    let url = this.apiUrl + 'api-token-auth/';
    return this.http.post(url, this.user, this.getHeaders()).pipe(
      tap((res: User) => {
        this.user = res;
        this._cookieService.put('user-token', this.user.token);
        this.isLoggedIn = true;
        this.user.password = null;
        return this.user;
      }),
      catchError(catchError(this.handleError()))
    );
  }

  getPictures(tag?: string): Observable<Picture[]> {
    let url = this.apiUrl + 'pictures/';
    if (tag) {
      url = url + '?tag=' + tag;
    }
    return this.http.get<Picture[]>(url, this.getHeaders()).pipe(
      tap((res: Picture[]) => res),
      catchError(catchError(this.handleError()))
    )
  }

  postPicture(image: string, desc: string): Observable<Picture> {
    let url = this.apiUrl + 'pictures/';
    return this.http.post<Picture>(url, {'image': image, 'desc': 'My picture or not?'}, this.getHeaders()).pipe(
      tap((res: Picture) => res),
      catchError(catchError(this.handleError()))
    )
  }

  putPicture(picture: Picture): Observable<Picture> {
    let url = this.apiUrl + 'pictures/' + picture.id + '/';
    return this.http.put<Picture>(url, {'desc': picture.desc}, this.getHeaders()).pipe(
      tap((res: Picture) => res),
      catchError(catchError(this.handleError()))
    )
  }

  deletePicture(id) {
    let url = this.apiUrl + 'pictures/' + id + '/';
    return this.http.delete(url, this.getHeaders()).pipe(
      tap((res: any) => res),
      catchError(catchError(this.handleError()))
    )
  }

  getPicture(id): Observable<Picture> {
    let url = this.apiUrl + 'pictures/' + id + '/';
    return this.http.get(url, this.getHeaders()).pipe(
      tap((res: Picture) => res),
      catchError(catchError(this.handleError()))
    )
  }

  public verifyToken() {
    let url = this.apiUrl + 'api-token-verify/';
    return this.http.post(url, {'token': this.user.token}, this.getHeaders()).pipe(
      tap((res: any) => res),
      catchError(catchError(this.handleError()))
    )
  }

  public registerUser(): Observable<User> {
    let url = this.apiUrl + 'users/';
    this.isLoggedIn = false;
    this.user.token = null;
    // TODO: add serializer
    return this.http.post<User>(url, {
      'username': this.user.username,
      'first_name': this.user.firstName,
      'last_name': this.user.lastName,
      'password': this.user.password
    }, this.getHeaders()).pipe(
      tap((res: User) => {
        this.user = res;
        this._cookieService.put('user-token', this.user.token);
        this.isLoggedIn = true;
        this.user.password = null;
        return this.user;
      }),
      catchError(catchError(this.handleError()))
    );
  }

  private handleError() {
    return (err: any) => {
      if (err instanceof HttpErrorResponse) {
        if (err.status === 401) {
          this.logout(true);
        }
        console.log(`status: ${err.status}, ${err.statusText}`);
      }
      return Observable.throw('error');
    }
  }
}
