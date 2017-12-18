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
        this.router.navigate(['/hotdogs']);

      },
      err => {
        this.showError('Failed, try again!', 'OK')
      }
    )
    event.preventDefault();
  }
}
