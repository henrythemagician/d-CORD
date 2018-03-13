node ('master') {
    stage 'Checkout code'
    checkout([$class: 'RepoScm', currentBranch: true, manifestRepositoryUrl: 'https://gerrit.opencord.org/manifest', quiet: true])
    
    stage 'Build and Publish apps'
    sh 'cd onos-apps && ./gradlew release'
}
