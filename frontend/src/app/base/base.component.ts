import {Component} from '@angular/core';
import {ApiService} from '../api.service';
import {Router} from '@angular/router';
import {MatDialog, MatSnackBar, MatSnackBarConfig} from '@angular/material';
import {Subscription} from "rxjs/Subscription";
import {SocketService} from "../socket.service";
import {Tag} from "../_models/tag.model";
import {Picture} from "../_models/picture.model";

@Component({
  selector: 'app-base',
  template: '',
})
export class BaseComponent {
  public _apiService: ApiService;
  public socketSubscription: Subscription;

  constructor(_apiService: ApiService, public router: Router, public snackBar: MatSnackBar, public dialog: MatDialog,
              public socket: SocketService) {
    this._apiService = _apiService;

    const stream = this.socket.connect();
    this.socketSubscription = stream.subscribe((message) => {
      this.handleSocketMessage(message);
    });
  }

  ngOnDestroy() {
    this.socketSubscription.unsubscribe()
  }

  showError(message: string, action: string, duration = 3000) {
    this.snackBar.open(message, action, <MatSnackBarConfig>{duration: duration, extraClasses: ['error-message']});
  }

  showSuccess(message: string, action: string, duration = 3000) {
    this.snackBar.open(message, action, <MatSnackBarConfig>{duration: duration, extraClasses: ['success-message']});
  }

  public handleSocketMessage(message: any) {
  }

  public goTag(tag: Tag) {
    if (tag && tag.name) {
      this.router.navigate(['/hotdogs', {tag: tag.name}]);
    }
  }

  public goPicture(picture: Picture) {
    if (picture && picture.id) {
      this.router.navigate(['/hotdog', {id: picture.id}]);
    }
  }
}
