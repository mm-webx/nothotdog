import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {BaseComponent} from "../base/base.component";
import {MatDialog, MatSnackBar} from "@angular/material";
import {ApiService} from "../api.service";
import {Picture} from "../_models/picture.model";
import {SocketService} from "../socket.service";

@Component({
  selector: 'app-hot-dog-details',
  templateUrl: './hot-dog-details.component.html',
  styleUrls: ['./hot-dog-details.component.scss']
})
export class HotDogDetailsComponent extends BaseComponent implements OnInit {
  public picture = new Picture;
  public sub: any;
  public loading = true;
  saveButtonDisabled = true;

  constructor(private route: ActivatedRoute, _apiService: ApiService, public router: Router, public snackBar: MatSnackBar, public dialog: MatDialog,
              public socket: SocketService) {
    super(_apiService, router, snackBar, dialog, socket);
  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.getDetails(params['id'])
    });
  }

  getDetails(id: string) {
    this._apiService.getPicture(id).subscribe(
      picture => {
        this.picture = picture;
        this.loading = false;
      },
      err => {
        this.picture = new Picture;
        this.loading = false;
        this.showError('Can\'t read data from server', 'OK', 3000);
        this.router.navigate(['/home']);
      }
    );
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  enableSave() {
    this.saveButtonDisabled = false;
  }


  deletePicture() {
    if (confirm("Want to delete?")) {
      this._apiService.deletePicture(this.picture.id).subscribe(
        pictures => {
          this.router.navigate(['/hotdogs']);
        },
        err => {
          this.showError('Can\'t delete picture.', 'OK')
        }
      );
    }
  }

  savePicture() {
    this._apiService.putPicture(this.picture).subscribe(
      picture => {
        this.picture = picture;
      },
      err => {
        this.picture = new Picture;
        this.loading = false;
        this.showError('Can\'t read data from server', 'OK', 3000);
        this.router.navigate(['/home']);
      }
    );
  }
}
