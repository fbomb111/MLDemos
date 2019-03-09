//
//  AppDelegate.swift
//  SentimentAnalyzer
//
//  Created by Frankie Cleary on 3/9/19.
//  Copyright © 2019 FbombMedia. All rights reserved.
//

import UIKit
import AWSCore

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Initialize the Amazon Cognito credentials provider
        // You can setup an identity pool at https://us-east-2.console.aws.amazon.com/cognito/pool?region=us-east-2 if you haven't already
        // Ensure you add the ComprehendFullAccess policy to your user roles
        // For this sample we've went with allowing unauthorized users
        let credentialsProvider = AWSCognitoCredentialsProvider(regionType:.USEast2,
                                                                identityPoolId:"us-east-2:644f1e51-d198-4ece-ba5b-a3e57cf89569")
        
        let configuration = AWSServiceConfiguration(region:.USEast2, credentialsProvider:credentialsProvider)
        
        AWSServiceManager.default().defaultServiceConfiguration = configuration
        
        return true
    }
}

