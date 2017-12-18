import {Component, OnInit} from '@angular/core';
import {BaseComponent} from "../base/base.component";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent extends BaseComponent implements OnInit {

  ngOnInit() {
    if (this._apiService.isLoggedIn) {
      this.router.navigate(['/hotdogs']);
    }
  }

  authUser(event: Event) {
    this._apiService.postAuth().subscribe(
      user => {
        this.router.navigate(['/hotdogs']);
      },
      err => {
        this.showError('Invalid username or password', 'OK');
      }
    );
    event.preventDefault();
  }

}
