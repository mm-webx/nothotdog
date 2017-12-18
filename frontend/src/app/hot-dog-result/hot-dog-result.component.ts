import {Component, OnInit} from '@angular/core';
import {BaseComponent} from "../base/base.component";

@Component({
  selector: 'app-hot-dog-result',
  templateUrl: './hot-dog-result.component.html',
  styleUrls: ['./hot-dog-result.component.scss']
})
export class HotDogResultComponent extends BaseComponent implements OnInit {

  ngOnInit() {
    if (!this._apiService.picture.id) {
      this.router.navigate(['/home']);
    }
  }

}
