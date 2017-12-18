import {Injectable} from "@angular/core";
import "rxjs/add/observable/of";
import "rxjs/add/operator/do";
import "rxjs/add/operator/delay";
import {Observable} from "rxjs/Observable";
import {QueueingSubject} from "queueing-subject";
import {WebSocketService} from "angular2-websocket-service";
import {environment} from "../environments/environment";
import 'rxjs/add/operator/share';

@Injectable()
export class SocketService {
  public outputStream: Observable<any>
  private inputStream: QueueingSubject<any>

  constructor(private socketFactory: WebSocketService) {
  }

  public connect() {
    if (this.outputStream) {
      return this.outputStream;
    }
    console.log(environment.socketUrl);
    // Using share() causes a single websocket to be created when the first
    // observer subscribes. This socket is shared with subsequent observers
    // and closed when the observer count falls to zero.
    return this.outputStream = this.socketFactory.connect(
      environment.socketUrl,
      this.inputStream = new QueueingSubject<any>()
    ).share();
  }

  public send(message: any): void {
    // If the websocket is not connected then the QueueingSubject will ensure
    // that messages are queued and delivered when the websocket reconnects.
    // A regular Subject can be used to discard messages sent when the websocket
    // is disconnected.
    console.log('chce', message);
    this.inputStream.next(message)
  }

}
