import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3Deploy from "aws-cdk-lib/aws-s3-deployment"
import * as greengrassv2 from 'aws-cdk-lib/aws-greengrassv2';

export class CdkGreengrassStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const deviceName = 'GreengrassCore-18163f7ac3e'
    const accountId = cdk.Stack.of(this).account
    // const bucketName = "gg-depolyment-storage"   // In the case of static s3 name

    // s3 deployment
    const s3Bucket = new s3.Bucket(this, "gg-depolyment-storage",{
      // bucketName: bucketName,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      publicReadAccess: false,
      versioned: false,
    });
    new cdk.CfnOutput(this, 'bucketName', {
      value: s3Bucket.bucketName,
      description: 'The nmae of bucket',
    });
    new cdk.CfnOutput(this, 's3Arn', {
      value: s3Bucket.bucketArn,
      description: 'The arn of s3',
    });
    new cdk.CfnOutput(this, 's3Path', {
      value: 's3://'+s3Bucket.bucketName,
      description: 'The path of s3',
    });

    // copy artifact into s3 bucket
    new s3Deploy.BucketDeployment(this, "UploadArtifact", {
      sources: [s3Deploy.Source.asset("../src")],
      destinationBucket: s3Bucket,
    }); 

    // components deployment
    const version_requester = "1.0.0", version_ImageClassifier = "1.0.0"
    const component = new customComponent(scope, "component", s3Bucket.bucketName, version_requester, version_ImageClassifier)    

    // deploy components
    const deployment = new componentDeployment(scope, "deployments", version_requester, version_ImageClassifier, accountId, deviceName)   
    deployment.addDependency(component); 
  }
}

export class customComponent extends cdk.Stack {
  constructor(scope: Construct, id: string, bucketName: string, version_requester: string, version_ImageClassifier: string, props?: cdk.StackProps) {    
    super(scope, id, props);

    // recipe of component - com.custom.requester
    const recipe_requester = `{
      "RecipeFormatVersion": "2020-01-25",
      "ComponentName": "com.custom.requester",
      "ComponentVersion": "${version_requester}",
      "ComponentDescription": "A component that requests the image classification.",
      "ComponentPublisher": "Amazon",
      "ComponentConfiguration": {
        "DefaultConfiguration": {
          "accessControl": {
            "aws.greengrass.ipc.pubsub": {
              "com.custom.requester:pubsub:1": {
                "policyDescription": "Allows access to publish/subscribe to the topics.",
                "operations": [
                  "aws.greengrass#PublishToTopic",
                  "aws.greengrass#SubscribeToTopic"  
                ],
                "resources": [
                  "local/inference",
                  "local/result"
                ]
              }
            }
          }
        }
      },
      "Manifests": [{
        "Platform": {
          "os": "linux"
        },
        "Lifecycle": {
          "Install": "pip3 install awsiotsdk",
          "Run": "python3 -u {artifacts:path}/publisher.py"
        },
        "Artifacts": [
          {
            "URI": "${'s3://'+bucketName}/requester/artifacts/com.custom.requester/1.0.0/requester.py"
          },
          {
            "URI": "${'s3://'+bucketName}/requester/artifacts/com.custom.requester/1.0.0/pelican.jpeg"
          }
        ]
      }]
    }`

    const cfnComponentVersion1 = new greengrassv2.CfnComponentVersion(this, 'MyCfnComponentVersion-requester', {
      inlineRecipe: recipe_requester,
    });

    new cdk.CfnOutput(this, 'componentName1', {
      value: cfnComponentVersion1.attrComponentName,
      description: 'The nmae of component',
    });  
    
    // recipe of component - com.custom.ImageClassifier
    const recipe_ImageClassifier = `{
      "RecipeFormatVersion": "2020-01-25",
      "ComponentName": "com.custom.ImageClassifier",
      "ComponentVersion": "${version_ImageClassifier}",
      "ComponentDescription": "A component that subscribe a topic from requester.",
      "ComponentPublisher": "Amazon",
      "ComponentConfiguration": {
        "DefaultConfiguration": {
          "accessControl": {
            "aws.greengrass.ipc.pubsub": {
              "com.custom.ImageClassifier:pubsub:1": {
                "policyDescription": "Allows access to subscribe/subscribe to the topics.",
                "operations": [
                  "aws.greengrass#PublishToTopic",
                  "aws.greengrass#SubscribeToTopic"     
                ],
                "resources": [
                  "local/inference",
                  "local/result"
                ]
              }
            }
          }
        }
      },
      "ComponentDependencies": {
        "variant.DLR.ImageClassification.ModelStore": {
          "VersionRequirement": ">=2.1.0 <2.2.0",
          "DependencyType": "HARD"
        }
      },
      "Manifests": [{
        "Platform": {
          "os": "linux"
        },
        "Lifecycle": {
          "Install": {
            "RequiresPrivilege": "true",
            "Script": "apt-get install libgl1 -y\\n pip3 install --upgrade pip\\n pip3 install scikit-build wheel opencv-python==4.6.0.66 dlr\\n python -m pip install dlr\\n pip3 install awsiotsdk"
          },
          "Run": {
            "RequiresPrivilege": "true",
            "Script": "python3 -u {artifacts:path}/interface.py"
          }
        },
        "Artifacts": [
          {
            "URI": "${'s3://'+bucketName}/classifier/artifacts/com.custom.ImageClassifier/1.0.0/classifier.py"
          },
          {
            "URI": "${'s3://'+bucketName}/classifier/artifacts/com.custom.ImageClassifier/1.0.0/inference.py"
          },
          {
            "URI": "${'s3://'+bucketName}/classifier/artifacts/com.custom.ImageClassifier/1.0.0/interface.py"
          }
        ]
      }]
    }`

    const cfnComponentVersion2 = new greengrassv2.CfnComponentVersion(this, 'MyCfnComponentVersion_ImageClassifier', {
      inlineRecipe: recipe_ImageClassifier,
    });

    new cdk.CfnOutput(this, 'componentName2', {
      value: cfnComponentVersion2.attrComponentName,
      description: 'The nmae of component',
    });     
  }
}

export class componentDeployment extends cdk.Stack {
  constructor(scope: Construct, id: string, version_requester: string, version_ImageClassifier: string, accountId: string, deviceName: string, props?: cdk.StackProps) {    
    super(scope, id, props);

        // deployments
    const cfnDeployment = new greengrassv2.CfnDeployment(this, 'MyCfnDeployment', {
      targetArn: `arn:aws:iot:ap-northeast-2:`+accountId+`:thing/`+deviceName,    
      components: {
      //  "com.custom.requester": {
      //    componentVersion: version_requester
      //  },
      //  "com.custom.ImageClassifier": {
      //    componentVersion: version_ImageClassifier
      //  },
        "aws.greengrass.Cli": {
          componentVersion: "2.9.2"
        }
      },
      deploymentName: 'deployment-ImageClassification',
      deploymentPolicies: {
        componentUpdatePolicy: {
          action: 'NOTIFY_COMPONENTS', // NOTIFY_COMPONENTS | SKIP_NOTIFY_COMPONENTS
          timeoutInSeconds: 60,
        },
        failureHandlingPolicy: 'ROLLBACK',  // ROLLBACK | DO_NOTHING
      },
    });   
  }
}