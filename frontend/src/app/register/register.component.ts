import {Component, OnInit} from '@angular/core';
import {BaseComponent} from "../base/base.component";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent extends BaseComponent implements OnInit {

  ngOnInit() {
    if (this._apiService.isLoggedIn) {
      this.router.navigate(['/hotdogs']);
    }
  }

  registerUser($event: Event) {
    this._apiService.registerUser().subscribe(
      user => {
        this.showSuccess('Account created, please log in!', 'OK');
        this.router.navigate(['/login']);
      },
      err => {
        this.showError('User exists or bad data', 'OK')
      }
    );
    event.preventDefault();
  }
}
