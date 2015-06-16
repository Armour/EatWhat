//
//  ViewController.m
//  YunGeZi
//
//  Created by Armour on 4/27/15.
//  Copyright (c) 2015 ZJU. All rights reserved.
//

#import "ViewController.h"
#import <QuartzCore/QuartzCore.h>
#import "WebViewController.h"

@interface ViewController ()

@property (strong, nonatomic) UIActivityIndicatorView *activityIndicator;
@property (strong, nonatomic) NSString *username;

@end


@implementation ViewController

enum {
    textUsernameTag = 0,
    textPasswordTag
};

- (BOOL)shouldAutorotate {
    return false;
}

- (void)prepareMyTextField {
    self.textUsername.delegate = self;
    self.textPassword.delegate = self;
    self.textUsername.tag = textUsernameTag;
    self.textPassword.tag = textPasswordTag;
    self.textUsername.layer.cornerRadius = 10.0f;
    self.textPassword.layer.cornerRadius = 10.0f;
    self.textUsername.layer.borderColor = [[UIColor lightGrayColor] CGColor];
    self.textPassword.layer.borderColor = [[UIColor lightGrayColor] CGColor];
    self.textUsername.layer.borderWidth = 1.0f;
    self.textPassword.layer.borderWidth = 1.0f;
    self.textUsername.clearButtonMode = UITextFieldViewModeWhileEditing;
    self.textPassword.clearButtonMode = UITextFieldViewModeWhileEditing;
}

- (void)prepareMyButton {
    [self.loginButton setBackgroundColor:[UIColor purpleColor]];
    self.loginButton.layer.cornerRadius = 10.0f;
}

- (IBAction)loginButtonTouchUpInside:(UIButton *)sender {
    [self.activityIndicator setHidden:NO];
    [self.activityIndicator startAnimating];
    dispatch_queue_t requestQueue = dispatch_queue_create("webRequestInLogin", NULL);
    dispatch_async(requestQueue, ^{
        NSInteger status = -1;
        @try {
            NSURL *postURL = [NSURL URLWithString:@"http://localhost:3002/users/login"];
            NSString *postStr = [NSString stringWithFormat:@"username=%@&password=%@", self.textUsername.text, self.textPassword.text];
            NSData *postData = [postStr dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES];
            NSString *postLength = [NSString stringWithFormat:@"%lu", (unsigned long)[postData length]];
            NSString *postContentType = @"application/x-www-form-urlencoded";

            NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
            [request setURL:postURL];
            [request setHTTPMethod:@"POST"];
            [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
            [request setValue:postContentType forHTTPHeaderField:@"Content-Type"];
            [request setHTTPShouldHandleCookies:YES];
            [request setHTTPBody:postData];

            NSError *requestError = [[NSError alloc] init];
            NSHTTPURLResponse *requestResponse;
            NSData *requestHandler = [NSURLConnection sendSynchronousRequest:request returningResponse:&requestResponse error:&requestError];
            NSError *jsonError = nil;
            NSDictionary *jsonData = [NSJSONSerialization
                                      JSONObjectWithData:requestHandler
                                      options:NSJSONReadingMutableContainers
                                      error:&jsonError];
            NSLog(@"Response with json ==> %@", jsonData);

            status = [jsonData[@"code"] integerValue];
        }
        @catch (NSException *exception) {
            [self.activityIndicator stopAnimating];
            [self.activityIndicator setHidden:TRUE];
            [self popAlert:@"Login Fail" withMessage:@"Your network sucks ╮(╯_╰)╭"];
        }
        dispatch_async(dispatch_get_main_queue(), ^{
            [self.activityIndicator stopAnimating];
            [self.activityIndicator setHidden:TRUE];
            if (status == 0) {
                self.username = self.textUsername.text;
                [self performSegueWithIdentifier:@"showWeb" sender:self];
            } else if (status == 1) {
                [self popAlert:@"Login Fail" withMessage:@"No username input ╮(╯_╰)╭"];
            } else if (status == 5) {
                [self popAlert:@"Login Fail" withMessage:@"Wrong password ╮(╯_╰)╭"];
            } else if (status == 6) {
                [self popAlert:@"Login Fail" withMessage:@"Username Does Not Exist ╮(╯_╰)╭"];
            }
        });
    });
}

- (void)addIndicator {
    self.activityIndicator = [[UIActivityIndicatorView alloc] initWithActivityIndicatorStyle:UIActivityIndicatorViewStyleGray];
    [self.activityIndicator setCenter:self.view.center];
    [self.activityIndicator setHidesWhenStopped:TRUE];
    [self.activityIndicator setHidden:YES];
    [self.view addSubview:self.activityIndicator];
    [self.view bringSubviewToFront:self.activityIndicator];
}

- (void)viewDidLoad {
    [super viewDidLoad];
    [self addIndicator];
    [self prepareMyButton];
    [self prepareMyTextField];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
}

-(BOOL)textFieldShouldBeginEditing:(UITextField *)textField {
    switch (textField.tag) {
        case textUsernameTag:
            self.textUsername.layer.borderColor = [[UIColor colorWithRed:0 green:204 blue:100 alpha:1] CGColor];
            break;
        case textPasswordTag:
            self.textPassword.layer.borderColor = [[UIColor colorWithRed:0 green:204 blue:100 alpha:1] CGColor];
            break;
        default:
            break;
    }
    return YES;
}

-(BOOL)textFieldShouldEndEditing:(UITextField *)textField {
    switch (textField.tag) {
        case textUsernameTag:
            self.textUsername.layer.borderColor = [[UIColor lightGrayColor] CGColor];
            break;
        case textPasswordTag:
            self.textPassword.layer.borderColor = [[UIColor lightGrayColor] CGColor];
            break;

        default:
            break;
    }
    return YES;
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    [textField resignFirstResponder];
    return YES;
}

- (IBAction)backgroundTap:(id)sender {
    [self.view endEditing:YES];
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    if([segue.identifier isEqualToString:@"showWeb"]){
        WebViewController *controller = (WebViewController *)segue.destinationViewController;
        [controller setUsername:self.username];
    }
}

- (void) popAlert:(NSString *)title withMessage:(NSString *)message {
    UIAlertView * alert =[[UIAlertView alloc] initWithTitle:title
                                                    message:message
                                                   delegate:self
                                          cancelButtonTitle:@"OK"
                                          otherButtonTitles: nil];
    [alert show];
}

@end
